import wikipedia as wk
wk.set_lang('en')

a= wk.page('Cuba')
print(a.title)

print(wk.search('Cuba'))


