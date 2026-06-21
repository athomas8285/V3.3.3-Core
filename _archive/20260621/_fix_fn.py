
import re
content = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Find the renderCompletedHistory function boundaries
fstart = content.index('function renderCompletedHistory(){')
fend = content.index('function scrollToDateGroup(', fstart)
# Remove everything between these
# Instead, let me find exact patterns and fix them

# Pattern 1: corrputed text in hist-empty
old1 = '<div class="hist-empty" style="padding:12px;font-size:12px;color:var(--t3);text-align:center;">'
idx1 = content.find(old1, fstart)
if idx1 >= 0:
    end1 = content.find("'", idx1 + len(old1) + 20)
    chunk = content[idx1:end1]
    # Replace with correct Chinese
    correct = '\\\\u6682\\\\u65e0\\\\u5df2\\\\u7ed3\\\\u675f\\\\u7684\\\\u6bd4\\\\u8d5b'
    # Actually let me just replace the whole thing
    print('Found hist-empty at', idx1)
    print('Chunk:', repr(chunk))

# Pattern 2: the hit/miss text after hitCount + '/' + total
old2 = "hitCount + '/' + total + '"
idx2 = content.find(old2, fstart)
if idx2 >= 0:
    end2 = content.find("</span>", idx2)
    chunk = content[idx2:end2]
    print('Found hit count at', idx2)
    print('Chunk:', repr(chunk))

print()
print('Function content:')
end_func = content.index('function scrollToDateGroup(label){', fstart)
end_func = content.index('function scrollToDateGroup(label){', end_func + 5)
fend = content.index('

', end_func) 
print(repr(content[fstart:fend]))
