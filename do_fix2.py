import sys
path = r'C:\Users\gjj\Desktop\v333\templates\charts.js'
with open(path, 'rb') as f:
    data = f.read()

# Search bytes: }).join(\'\') +\'</div></div>\' +\'<span class="sec-l"></span></div>\';
# In the actual file, the single quotes inside JS strings are NOT escaped
# Let's search for the exact bytes
old_bytes = b'}).join(\'\') +\'</div></div>\' +\'<span class="sec-l"></span></div>\';'
# Actually in raw bytes, since we read with 'rb', we need to think about what's in the file
# The file has literal single quotes
# Let me build the exact byte sequence

# Looking at the repr output: \') +\'</div></div>\' +\'<span class="sec-l"></span></div>\';
# This means the actual bytes are: ' )   + ' < / d i v > ...
# Hmm, but that doesn't make sense for JS join('').

# Let me just search for a unique substring:
# join('') +'</div></div>'
sub = b"join('') +'</div></div>'"
idx = data.find(sub)
print("join found at offset:", idx)
if idx >= 0:
    print("Context:", data[idx-20:idx+60])
else:
    print("Not found")