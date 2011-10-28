module(..., package.seeall);

function send(endpoint, data, timeout)
end

function read(endpoint, len, timeout)
end


function init(baseboards)
	--parameters sanity check
	assert(type(baseboards)=="table")

	local n_boards=1
	--local bb = bobot_baseboard.BaseBoard:new({idBoard=iSerial, comms=comms_usb})
	local bb = {idBoard=1, comms=comms_chotox}
	local devices={}
	for i, name in ipairs({"led","led1","grises","grises1","dist","temp","butia","display","butia"}) do
		local dd={name=name, baseboard=bb,api={},handler=i}
		dd.open = function() return true end
		dd.close = function() end
		dd.read = function() return "" end
		dd.send = function() return true end
		devices[name]=dd
	end
	bb.devices=devices
	baseboards[1]=bb
	return n_boards
end


