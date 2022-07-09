lrc_file = open(input("lrc file : ").strip())
lrc_string = ''.join(lrc_file.readlines())
lrc_file.close()

subs = pylrc.parse(lrc_string)

print('Playing "' + subs.title + '" by "' + subs.artist + '"')

num_lines = len(subs)

    if line+1 == num_lines or sec < subs[line+1].time:

            print(subs[line].text.rstrip() + " " * (60 - len(subs[line].text)))
