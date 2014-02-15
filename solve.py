#  http://geekdad.com/2014/02/geekdad-puzzle-functional-numeric-wordsearch/

#OCR'd from .jpg at URL above

data = """1447417662 58237947657 223488277
6726847322 31423247811 172848323
1923426437 11275787699 783297276
3865523675 94427165956 822354733
2453463797 32793163461 257167185
8524949633 81948134437 427421213
5886334564 72894144753 281469837
8798769759 59435211846 121214978
4499141767 91817274142 629572773
1798615499 35426778726 598765747
2555723511 69235796239 614341434
5848515486 19197534343 393527298
1864135546 91832214658 792796748
8134129284 22638829429 565163389
7127847449 86211949456 746436335
7646158875 98741755361 316815492
9423494286 93877298824 625748883
4244392134 78275639884 354362176
8942911228 35185582419 922998719
3845229884 28323785959 657434567
1736394571 98718721348 693774783
9968169533 22599258644 251286799
6454882237 82147386198 275492589
3187298664 54667499552 396342828
2681445177 93269739171 476194554
1131816167 48618866613 771892436
8771995421 18188195997 937547338
6149668949 54941266852 355678369
3489763828 16684259142 244792732
1816726588 62446422894 458679165"""
   
def apply_template(x,y,template,values,width,height):
    idxs = []
    vals = []
    for dx,dy in template:
        i = (x+dx,y+dy)
        if i[0] > width or i[0] < 0 or i[1] > height or i[1] < 0:
            return None,None
        else:
            idxs.append(i)
            # looks backwards but it's not, need to find right row before indexing over to column
            vals.append(values[i[1]][i[0]])  
    return idxs,vals

def calc(vals,idxs,tn):
    a,b,c,d,e = vals
    results = (a+b)*c - (d*e)
    return results,tn,tuple(vals),tuple(idxs)

def format_record(rec):
    result,desc,values,idxs = rec
    if desc == 'row':
        desc = 'horizontally right to left'
    elif desc == 'rowrev':
        desc = 'horizontally left to right'
    elif desc == 'col':
        desc = 'vertically top to bottom'
    elif desc == 'colrev':
        desc = 'vertically bottom to top'
    elif desc == 'down_left':
        desc = 'diagonally down to the left'
    elif desc == 'down_leftrev':
        desc = 'diagonally up to the right'
    elif desc == 'down_right':
        desc = 'diagonally down to the right'
    elif desc == 'down_rightrev':
        desc = 'diagonally up to the left'
    equation = "(%i + %i) * %i - %i * %i = %i" % (values+(result,))
    start = "%i,%i" % (idxs[0][0] + 1,idxs[0][1] + 1)
    return result,equation,desc,start
    

a = []
lines = data.split('\n')
h = len(lines)
w = None
for line in lines:
    line = list(int(x) for x in line.replace(' ',''))
    if w is None:
        w = len(line)
    a.append(line)



templates = []
# each of these describe a recipe for finding
# a line of 5 numbers by applying each tuple in turn
# to a starting tuple
row_t = ((0,0),(1,0),(2,0),(3,0),(4,0))
col_t = ((0,0),(0,1),(0,2),(0,3),(0,4))
down_left_t = ((0,0),(-1,1),(-2,2),(-3,3),(-4,4))
down_right_t = ((0,0),(1,1),(2,2),(3,3),(4,4))
templates.extend((row_t,col_t,down_left_t,down_right_t))

output = []
keyset = set()
for y in range(h):
    for x in range(w):
        for t,tn in zip(templates,('row','col','down_left','down_right')):
            idxs,vals = apply_template(x,y,t,a,w-1,h-1)
            if vals is None:
                # at least one of the index pairs went off the grid
                continue
            else:
                if tuple(idxs) in keyset:
                    # we might have already seen this example
                    continue
                output.append(calc(vals,idxs,tn))
                keyset.add(tuple(idxs))
                # apply the values from the same 'line' backwards
                vals.reverse()
                idxs.reverse()
                output.append(calc(vals,idxs,tn+'rev'))
                keyset.add(tuple(idxs))

# result is first item in tuple so 
# it will be sorted on that
output.sort()

result,equation,desc,start = format_record(output[0])
print "Lowest value is %i starting at %s and moving %s." % (result,start,desc)
print equation

result,equation,desc,start = format_record(output[-1])
print "Highest value is %i starting at %s and moving %s." % (result,start,desc)
print equation

zeros = [o for o in output if o[0] == 0]
count_zero = len(zeros)
print "There are %i sets that result in 0." % count_zero
for x in zeros:
    _,equation,desc,start = format_record(x)
    print "%s starting at %s and moving %s." % (equation,start,desc)
