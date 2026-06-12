c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Check the page structure near the bottom
# Find the footer section
fe = c.rfind('</footer>')
# Look backwards from footer to understand its container
before = c[fe-200:fe+20]
print('Before header (last 200 chars before footer):')
print(repr(before))

# Check if there's an unclosed tag issue
# Find the main div containers
print()
print('Looking for page structure issues...')

# Check for common issues - check for !@#$%^&* characters outside of tags
# Just show what comes right before </footer>
pre_footer = c.rfind('<footer')
print('Footer starts at:', pre_footer)
print('Footer content (first 100):', repr(c[pre_footer:pre_footer+100]))