def execs(code,num_type=float):
	m={}
	lines=code.splitlines()
	for i in lines:
		if i.strip():
			ltk=[j.strip() for j in i.split()]
		else:
			continue
		head=ltk[0]
		if head=="WT":
			m[ltk[1]]=num_type(ltk[2])
		elif head=="ADD":
			m[ltk[1]]+=m[ltk[2]]
		elif head=="SUB":
			m[ltk[1]]-=m[ltk[2]]
		elif head=="MUL":
			m[ltk[1]]*=m[ltk[2]]
		elif head=="DIV":
			m[ltk[1]]/=m[ltk[2]]
		elif head=="MOD":
			m[ltk[1]]%=m[ltk[2]]
		elif head=="COPY":
			m[ltk[1]]=m[ltk[2]]
		elif head=="FREE":
			del m[ltk[1]]
		elif head=="POW":
			m[ltk[1]]**=m[ltk[2]]
		elif head=="RD":
			print(m.get(ltk[1]))
		else:
			print(f"Error:{repr(head)} is not in command_list.We have WT,ADD,SUB,MUL,DIV,MOD,COPY,FREE,POW,RD.Line_tokens:{ltk}")
	return m
yyy_decoder={"读一读":"RD","写一写":"WT","加一加":"ADD","减一减":"SUB","乘一乘":"MUL","除一除":"DIV","取个模":"MOD","多次乘":"POW","清空":"FREE","复制":"COPY"}
easy_decoder={"W":"WT","R":"RD","A":"ADD","S":"SUB","MU":"MUL","D":"DIV","MO":"MOD","P":"POW","C":"COPY","F":"FREE"}
def compiles(code,decoder):
	for i in decoder.keys():
		code=code.replace(i,decoder.get(i))
	return code
if __name__=="__main__":
	print(compiles("""
	写一写 0x00 123
	写一写 0x01 1.1
	加一加 0x00 0x01
	读一读 0x00
	清空 0x00
	清空 0x01
	""",yyy_decoder))
	m=execs("""
	WT 0x01 10
	WT 0x02 2
	POW 0x01 0x02
	RD 0x01
	FREE 0x01
	FREE 0x02
	ABC 1
	""")