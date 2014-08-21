d = read.csv('si_raw.csv')
dTrue = d[d$answer == 1, ]
tPersent = table(dTrue$image, dTrue$description) / table(d$image, d$description)
barplot(tPersent, beside=TRUE, legend.text=TRUE)
