#!/usr/bin/env Rscript

# Output to PDF file r_normalplot.pdf
pdf("../img/r_normalplot.pdf")

x <- seq(-4, 4, length=100)
px <- pnorm(x)
dx <- dnorm(x)

plot(x, dx, type="l", lty=2, xlab="x",
  ylab="pnorm(x) dnorm(x)", main="R pnorm and dnorm distribution",
  xlim=c(-4, 4), ylim=c(0, 1.1))

lines(x, px, lwd=2)
legend(-4,1, c("pnorm(x)","dnorm(x)"), lty=c(1,2))

dev.off()
q()

