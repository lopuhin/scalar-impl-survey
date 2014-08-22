library(boot)
library(ggplot2)

## clean up environment
rm(list=ls())


getTruePersent = function (d) {
    dTrue = d[d$answer == 1, ] # true answers
    tTrue = table(dTrue$image, dTrue$description)
    tAll = table(d$image, d$description)
    ## persent of true answers
    return(tTrue / tAll)
}

getTruePersentBootstrap = function (data, indices) {
    return(getTruePersent(data[indices,]))
}


full_data = read.csv('si_raw.csv')

bs = boot(full_data, getTruePersentBootstrap, R=100)

tPersent = getTruePersent(full_data)
dPersent = as.data.frame(tPersent)
colnames(dPersent) = c('image', 'description', 'answer')

dPersent$sd = apply(bs$t, 2, sd)

print(ggplot(
    dPersent,
    aes(x=description, fill=image)) +
    geom_bar(
        aes(y=answer),
        position=position_dodge(width=0.9),
        size=0.2,
        colour='black',
        stat='identity') +
    geom_errorbar(
        aes(ymin=answer-sd, ymax=answer+sd),
        position=position_dodge(width=0.9),
        size=0.2,
        width=0.2)
      )
