
dynamixel_id = 1
length = 5
instruction = 3
P1 = 30
P2 = 32
P3 = 3

Checksum = (0x02+0x30+0x30+0x81+0x56+0x8B+0x82) & 0xff

#Checksum = hex(~(0x01+0x05+0x03+0x1E+0x32+0x03) & 0xff)

Checksum = hex(~(0x01+0x05+0x03+0x1E+0xCD+0x00) & 0xff)

Checksum_0 =   hex(~(0x01+0x05+0x03+0x1E+0x00+0x00) & 0xff)
Checksum_60 =  hex(~(0x01+0x05+0x03+0x1E+0xCC+0x00) & 0xff)
Checksum_120 = hex(~(0x01+0x05+0x03+0x1E+0x99+0x01) & 0xff)
Checksum_180 = hex(~(0x01+0x05+0x03+0x1E+0x66+0x02) & 0xff)
Checksum_240 = hex(~(0x01+0x05+0x03+0x1E+0x33+0x03) & 0xff)
Checksum_300 = hex(~(0x01+0x05+0x03+0x1E+0x00+0x04) & 0xff)


a = "0x02"

b = int(a, 16)


print(Checksum_0)
print(Checksum_60)
print(Checksum_120)
print(Checksum_180)
print(Checksum_240)
print(Checksum_300)

print(2.31//1)



def angle_to_instruction(angle):

	A = int(angle / 300 * 1024)  # map to 10-bit number 

	B = A/256               # seperate into 2 8 bit bytes by dividing by max value of 8 bit byte 

	H = int(B // 1)         # decimal value of high byte, convert to intager
	print(H)

	L = B - H                     
	print(L)
	L = int(L * 256)        # decimal value of low byte

	
	H = hex(H)

	L = hex(L)

	return(H, L)

def angle_to_instruction_(angle):

	A = int(angle / 300 * 1024)  # map to 10-bit number 

	h = A >> 8         # decimal value of high byte, convert to intager
	print(h)

	l = A                     
	print(l)
	
	h = hex(h)

	l = hex(l)

	return(h, l)


a = angle_to_instruction(60)
print(a)
# print(type(a[0]), type(a[1]))
# print(type(0x01))

b = angle_to_instruction_(60)
print(b)
# TODO add hex strings to instruction packet to send to motor

# TODO calculate checksum using instruction packet then send to motor  
def move(servo_id, position):

	P = position  # position as 10-bit number 

	h = P >> 8    # value of high 8 bit byte

	l = P & 0xff        # value of low 8-bit byte                 
	
	print('check', format(h, '#04x'),format(l, '#04x')) # print full hex string representation 
	
# 	checksum = hex(~(servo_id +
#                      ax_goal_length + 
#                      ax_write_data +
#                      0x1E + h + l)
#                    & 0xff)
	
	checksum = ~(servo_id + ax_goal_length + ax_write_data + 0x1E + h + l) & 0xff
	checksum = format(checksum, '#04x') 
#                        
#     checksum = format(checksum, '#04x')       
	
	
	
	print(checksum)
	
	instruction_packet = (format(ax_start, '02x') + " " +
                          format(ax_start, '02x') + " " +
                          format(servo_id, '02x') + " " + 
                          format(ax_goal_length, '02x') + " " +
                          format(ax_write_data, '02x') + " " +
                          format(0x1E, '02x') + " " +
                          format(l, '02x') + " " +
                          format(h, '02x') + " " +
                          checksum[2:] 
                          ).upper()
                          #str(ax_write_data) + str(0x1E) + str(l) + str(h) + str(checksum))

	return(instruction_packet)

ax_start = 0xff
ax_id = 0x01
ax_goal_length = 0x05
ax_write_data = 0x03
print(move(ax_id, 0))
print(move(ax_id, int(60/300 * 1024)))
print(move(ax_id, int(120/300 * 1024)))