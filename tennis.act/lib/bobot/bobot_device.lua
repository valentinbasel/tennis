module(..., package.seeall);

local string_char = string.char
local string_len  = string.len
local string_byte = string.byte

local OPEN_COMMAND			= string_char(0x00)
local CLOSE_COMMAND         		= string_char(0x01)
local HEADER_PACKET_SIZE	        = 6
local NULL_BYTE         		= string_char(0x00)
local ADMIN_MODULE_IN_ENDPOINT  	= 0x01
local ADMIN_MODULE_OUT_ENDPOINT		= 0x81
local ADMIN_HANDLER_SEND_COMMAND	= string_char(0x00)
local OPEN_RESPONSE_PACKET_SIZE		= 5 
local CLOSE_RESPONSE_PACKET_SIZE	= 2 
local TIMEOUT				= 200 --ms

local READ_HEADER_SIZE		        = 3

local my_path = debug.getinfo(1, "S").source:match[[^@?(.*[\/])[^\/]-$]]

Device = {
	--some usefull stuff for the drivers to use
	string=string,
	print=print,
	math=math,
	tonumber=tonumber,
	tostring=tostring
}

local function load_driver(modulename)
	local drivername=string.match(modulename, '^(.-)%d*$')
	local f, err = loadfile(my_path.."../drivers/"..drivername..".lua")
	return f, err
end

--Instantiates Device object.
--Attempts to load api from driver
function Device:new(d)
	--parameters sanity check
	assert(type(d)=="table")
	assert(type(d.name)=="string")
	assert(type(d.baseboard)=="table")
	assert(type(d.baseboard.comms)=="table")
	assert(type(d.baseboard.comms.send)=="function")
	assert(type(d.baseboard.comms.read)=="function")
	
 	--OO boilerplate
  	setmetatable(d, self)
	self.__index = self

	--store locally, save 2 indirections
	d.comms_send = d.baseboard.comms.send
	d.comms_read = d.baseboard.comms.read

	--attempt to load api from driver
	local f, err = load_driver(d.name)
	if f then
		d._G=d
		
		setfenv(f, d) --the driver's environment is the device
		local status, err=pcall(f) 
		if status then
			print("u4d:new:Success loading driver:", d.name)
		else
			print("u4d:new:Error initializing driver:", tostring(err))
		end
	else
		print("u4d:new:Error loading driver:", err)
	end
	
	return d
end

--opens the device. must be done before sending / reading / etc.
--receives endpoints, which can be ommited if they were provided at Device creation
function Device:open(in_endpoint, out_endpoint)
	--state & parameter sanity check
	assert(self.handler==nil)
	assert(type(self.name)=="string")
	assert(type(in_endpoint)=="number" or type(self.in_endpoint)=="number")
	assert(type(self.comms_send)=="function")
	assert(type(self.comms_read)=="function")
	assert(type(out_endpoint)=="number" or type(self.out_endpoint)=="number")

	--save for later use
	if in_endpoint then self.in_endpoint = in_endpoint end
	if out_endpoint then self.out_endpoint = out_endpoint end

	local module_name=self.name .."\000" -- usb4all expect null terminated names

	local open_packet_length = string_char(HEADER_PACKET_SIZE + string_len(module_name)) 

	local module_in_endpoint  = string_char(self.in_endpoint)
	local module_out_endpoint = string_char(self.out_endpoint)

	local handler_packet = ADMIN_HANDLER_SEND_COMMAND .. open_packet_length .. NULL_BYTE
	local admin_packet = OPEN_COMMAND .. module_in_endpoint .. module_out_endpoint .. module_name	
	local open_packet  = handler_packet .. admin_packet
	local write_res = self.comms_send(ADMIN_MODULE_IN_ENDPOINT, open_packet, TIMEOUT)

	if not write_res then
		print("u4d:open:comunication with I/O board write error", write_res)
		return false
	end

	local data, err = self.comms_read(ADMIN_MODULE_OUT_ENDPOINT, OPEN_RESPONSE_PACKET_SIZE, TIMEOUT)	
	if not data then
		print ("u4d:open:comunication with I/O boardread error", err)
		return false 
	end

	local handler = string_byte(data, 5)
	--hander -1 meand error
	if handler==255 then
		print ("u4d:open:Already open!",self.name,self.handler)
		return
	else
		print ("u4d:open:Success!",self.name,handler)
		self.handler = handler --self.handler set means device is open
		return true
	end

end

--closes the device
function Device:close()
	if not self.handler then return end	--already closed

	--state sanity check
	assert(type(self.handler)=="number")
	assert(type(self.comms_send)=="function")
	assert(type(self.comms_read)=="function")

	local close_packet_length = string_char(0x04) --string.char(HEADER_PACKET_SIZE + string.len(module_name))
	local handler_packet = ADMIN_HANDLER_SEND_COMMAND .. close_packet_length .. NULL_BYTE
	local admin_packet = CLOSE_COMMAND .. string_char(self.handler)
	local close_packet  = handler_packet .. admin_packet

	local write_res = self.comms_send(ADMIN_MODULE_IN_ENDPOINT, close_packet, TIMEOUT)
	if not write_res then
		print("u4d:close:comunication with I/O board write error", write_res)
		return
	end
	local data, err = self.comms_read(ADMIN_MODULE_OUT_ENDPOINT, CLOSE_RESPONSE_PACKET_SIZE, TIMEOUT)

	self.handler = nil
end

--sends data (a string) to device
function Device:send(data)
	--state & parameter sanity check
	assert(type(data)=="string")
	assert(type(self.handler)=="number")
	assert(type(self.in_endpoint)=="number")
	assert(type(self.comms_send)=="function")
	assert(type(self.comms_read)=="function")

	local len=string_len(data)

	local shifted_handler = self.handler * 8	
    assert(shifted_handler<256, "u4d:send:shifted_handler vale " .. shifted_handler .. " excede el tamaño maximo representable en un byte (255)")	
    local user_module_handler_send_command = string_char(shifted_handler)   
	local send_packet_length = string_char(0x03 + len)	
	local send_packet = user_module_handler_send_command .. send_packet_length .. NULL_BYTE .. data	

	--local tini=socket.gettime()
	local write_res, err = self.comms_send(self.in_endpoint, send_packet, TIMEOUT)
	--print ('%%%%%%%%%%%%%%%% device send',socket.gettime()-tini)

	if not write_res then
		print("u4d:send:comunication with I/O board write error", err)	
	end

	return write_res, err
end

--read data (len bytes max) from device
function Device:read(len)
	len = len or 255
	--state & parameter sanity check
	assert(type(len)=="number")
	assert(type(self.handler)=="number")
	assert(type(self.out_endpoint)=="number")
	assert(type(self.comms_send)=="function")
	assert(type(self.comms_read)=="function")

	local data, err = self.comms_read(self.out_endpoint, len+READ_HEADER_SIZE, TIMEOUT)
	if not data then
		print("u4d:read:comunication with I/O board read error", err)	
		return nil, err
	end

	local data_h = string.sub(data, READ_HEADER_SIZE+1, -1) --discard header

	return data_h, err
end
