pdf("xx.pdf")
x <- seq(0,19, length = 300)
degf <- c(1,2,3,4,5,6,7)
labels <- c("df=1", "df=2", "df=3", "df=4", "df=5", "df=6", "df=7")
hx = dchisq(x, df=1)
plot(x, hx, type="l", lty=2, ylim=c(0.0,0.6),xlab="Chi-Square Error Value", ylab="Probability",main="Chi Square Distributions")
for (i in 1:7) {
	lines(x, dchisq(x,degf[i]), lwd=2, col="black")
}


