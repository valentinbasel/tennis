#!/usr/bin/lua

local socket = require("socket")

--local host, port = "192.168.10.1", 2009
local host, port = "localhost", 2009

local client = assert(socket.connect(host, port))
client:settimeout(nil) --blocking
--client:settimeout(1)

local function send(s)
	print("sending", s)
	client:send(s.."\n")
	local ret = client:receive()
	print("ret:", ret)
	return ret
end
send("LIST")
local ret = send("OPEN ledR")
print("el handler del ledR es " .. ret)
while true do
	send("CALL ledR prender")
	socket.sleep(0.5)
	send("CALL ledR apagar")
	socket.sleep(0.5)
end
