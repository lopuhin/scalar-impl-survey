library(boot)
library(ggplot2)

## clean up environment
rm(list=ls())


getTruePersent = function (d) {
    dTrue = d[d$answer == 1, ] # true answers
    tTrue = table(dTrue$image, dTrue$description)
    tAll = table(d$image, d$description)
    ## persent of true answers
    return(100.0 * tTrue / tAll)
}

getTruePersentBootstrap = function (data, indices) {
    return(getTruePersent(data[indices,]))
}


full_data = read.csv('si_raw.csv')

bs = boot(full_data, getTruePersentBootstrap, R=100)

tPersent = getTruePersent(full_data)
dPersent = as.data.frame(tPersent)
colnames(dPersent) = c('Meaning', 'Description', 'Answer')
dPersent$Meaning = factor(dPersent$Meaning,
        levels=c('false', 'local', 'literal', 'all'))
dPersent$sd = apply(bs$t, 2, sd) # FIXME - maybe * 1.96?

print(ggplot(
    dPersent,
    aes(x=Description, fill=Meaning)) +
    geom_bar(
        aes(y=Answer),
        position=position_dodge(width=0.9),
        size=0.2,
        colour='black',
        stat='identity') +
    geom_errorbar(
        aes(ymin=Answer-sd, ymax=Answer+sd),
        position=position_dodge(width=0.9),
        size=0.2,
        width=0.2) +
    ylab('True answer, %') +
    xlab('"Some" translation') +
    ggtitle('Preferances for meanings\ndepending on "some" translation') +
    theme_bw()
      )
