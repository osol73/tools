import crc32c

DEVICE="/dev/vda1"
OUTPUT="vda1-superblock-checksum.bin"

def calculateSuperblockChecksumByte ( pathToDevice, outFile ):
    # get superblock
    file = open(pathToDevice, "rb")
    sb_offset = 0x400
    file.seek(sb_offset)
    superblock = file.read(1024)
    file.close()

    # get superblock without checksum
    superblock_clean = superblock[0:0x3FC]

    # get superblock checksum original
    superblock_checksum_orig = superblock[0x3FC:0x3FC+4]

    # backup superblock checksum original
    print(f"Backup Original Checksum to {OUTPUT}.backup")
    file = open(OUTPUT + ".backup", "wb")
    file.write(superblock_checksum_orig)
    file.close()

    # generate superblock checksum
    inverter = 0xFFFFFFFF
    checksum = inverter - crc32c.crc32c(superblock_clean)
    checksum_hex = hex(checksum)[2:]
    if len(checksum_hex) % 2 != 0:
        checksum_hex = '0' + checksum_hex
    checksum_byte = bytes.fromhex(checksum_hex)
    checksum_byte = checksum_byte[::-1]

    # generate superblock checksum file
    print(f"Generate Checksum to {OUTPUT}")
    file = open(OUTPUT, "wb")
    file.write(checksum_byte)
    file.close()

calculateSuperblockChecksumByte(DEVICE, OUTPUT)