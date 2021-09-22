# This script automates the steps of the following video:
# https://www.youtube.com/watch?v=5F_fIlNYfPQ

with open("data/original.ogg", 'rb') as f:
    dnpt_data = f.read()

with open("data/void.ogg", "rb") as f:
    void_data = f.read()

with open("1.ogg", "rb") as f:
    ogg1_data = f.read()

with open("2.ogg", "rb") as f:
    ogg2_data = f.read()

# This function is used in step 3
def findnth(string, sub, n):
    '''Returns the index of the nth occurence (starting from 1) of a substring in a string.'''
    if n > string.count(sub) or n < 1:
        return None
    parts = string.split(sub)
    before_occ = sub.join(parts[:n])
    return len(before_occ)

# Step 1: Delete the first block (0:40 -> 0:45)
dnpt_data = dnpt_data[0x2DA8 + 1:]

# Step 2: Paste the data of 1.ogg (0:46 -> 0:53)
dnpt_data = ogg1_data + dnpt_data

# Step 3: Find the second occurence of OggS (0:54 -> 1:04)
len1 = len(ogg1_data)
sec_oggs_index = len1 + findnth(dnpt_data[len1:], b"OggS", 2)

# Step 4: Replace the old header with the new one (1:05 -> 1:53)
new_head = b"OggS" + ogg1_data.split(b"OggS")[-1] # Last header of 1.ogg
dnpt_data = dnpt_data[:sec_oggs_index] + new_head + dnpt_data[sec_oggs_index + 0xDB5:]

# Step 5: Delete 4F67675300020000000000000000B65D00000000 and everything below it (1:54 -> 2:13)
x = bytes.fromhex("4f67675300020000000000000000b65d00000000")
dnpt_data = dnpt_data.split(x)[0]

# Step 6: Paste the data of 2.ogg (2:14 -> 2:22)
dnpt_data += ogg2_data

# Step 7: Paste the data of void.ogg (2:23 -> 2:29)
dnpt_data += void_data

with open("DO_NOT_PLAY_THIS_AUDIO_FILE_TWICE.ogg", "wb") as f:
    f.write(dnpt_data)