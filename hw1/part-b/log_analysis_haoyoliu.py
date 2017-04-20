import re

with open('access_log.txt', 'rU') as f:
    valid_result = {}
    invalid_result = []
    for line in f:
        data = line.split()[6]

        # Determine if a line is valid
        if re.search(r'"GET|"POST', line) and re.search(r'" 200 {1}', line) and \
                re.search(r'T http://[A-Za-z]+|https://[A-Za-z]+', line) and \
                re.search(r'//[^/^:]+([A-Za-z]+|\d+)\.[A-Za-z]+', data):
            # Get date
            temp = re.search(r'\[[^"]*\]', line)
            date = temp.group().split(':')[0].replace('[', '')
            if date not in valid_result:
                valid_result[date] = {}

            # Get domain
            domains = re.findall(r'\.([a-zA-Z]+)[:?\d*]*[/| |"]', line)
            domain = domains[0].lower()

            # Counting
            if domain not in valid_result[date]:
                valid_result[date][domain] = 1
            else:
                valid_result[date][domain] += 1

        else:
            invalid_result.append(line)

# Sorting
for key, value in valid_result.items():
    valid_result[key] = sorted(value.items(), key=lambda x:x[0])
sorted_valid_result = sorted(valid_result.items(), key=lambda x:x[0])

with open('valid_log_summary_haoyoliu.txt', 'w') as outf:
    for tuple in sorted_valid_result:
        outstr = ''
        for item in tuple[1]:
            outstr += '{}:{}\t'.format(item[0], item[1])
        l = list(outstr)
        l.pop()
        outstr = ''.join(l)
        outstr = '{}\t{}\n'.format(tuple[0], outstr)
        outf.write(outstr)

with open('invalid_access_log_haoyoliu.txt', 'w') as outf1:
    for line in invalid_result:
        outf1.write(line)
