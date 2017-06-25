import re
from pexpect import pxssh
import pexpect
import getpass

def cis_sw_int(ses,monobj):
	try:
		out = {}
		mon_ = monobj.get("monitor")
		mon_ = mon_.split(",")
		for m in mon_:
			out.update({m:""})

		type_ = monobj.get("type")
		in_ = monobj.get("name")

		exp = ses[1]
		cmd = "show interface "+in_
		ses[0].sendline("terminal length 0")
		ses[0].sendline(cmd)
		ses[0].expect([cmd,pxssh.TIMEOUT],timeout=5)
		ses[0].expect([exp,pxssh.TIMEOUT],timeout=5)
		data = str(ses[0].before)
		if data.find("line protocol is up") == -1:
			# Interface down
			return "down"
		if "bits" in mon_:

			redata = re.findall(r'input rate [0-9]+|output rate [0-9]+',data)

			if len(redata) == 2:
				irate = redata[0].replace('input rate ','')
				orate = redata[1].replace('output rate ','')
				rate = irate+"|"+orate
				out.update({"bits":rate})
		
		if "duplex" in mon_:
			redata = re.findall(r'[a-zA-Z]+-duplex',data)
			if len(redata) > 0:
				out.update({"duplex":redata[0]})

		if "speed" in mon_:
			redata = re.findall(r'[0-9]+Mb/s',data)
			if len(redata) > 0:
				out.update({"speed":redata[0]})

		err = ""
		if "error" in mon_:
			redata = re.findall(r'Total output drops: [0-9]+',data)
			if len(redata) == 1:
				outdrop = redata[0].replace('Total output drops: ','')
				err = "drop:"+outdrop

			redata = re.findall(r'[0-9]+ input errors',data)
			if len(redata) == 1:
				inerror = redata[0].replace(' input errors','')
				err = err+"|"+inerror

			redata = re.findall(r'[0-9]+ CRC,',data)
			if len(redata) == 1:
				crcerror = redata[0].replace(' CRC,','')
				err = err+"|"+crcerror
				
			out.update({"error":err})

		return out
	except Exception as e:
		print("Error cis_sw_int"+str(e))



if __name__ == "__main__":
	pass;