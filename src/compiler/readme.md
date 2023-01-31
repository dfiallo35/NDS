<h2>Ejemplos de Códigos</h2>

<h4>Vars</h4>

```
#interger
var= 1;

#decimal
var= 1.4;

#boolean
var= true;
var= false;

#time
var= 1d;
var= 1m;
var= 1y;

#string
var= 'string';

#list
var= [1, 'string', 1.4, 6d, true, 5];

```

<h4>Elements</h4>

```
category <name>();

trait <name>();

nation <name>(<polulation>, <extension>, <trait list>, <neighbour list>, **hwargs);

sea <name>( <extension>, <neighbour list>);

```

<h4>Distribution</h4>

```
distribution <name>(<dist>, **kwargs);

#Distribuciones ya existentes
dist= ['alpha', 'anglit', 'arcsine', 'argus', 'bernoulli', 'beta', 'betabinom', 'betaprime', 'binom', 'boltzmann', 'bradford', 'burr', 'burr12', 'cauchy', 'chi', 'chi2', 'cosine', 'crystalball', 'dgamma', 'dlaplace', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponpow', 'exponweib', 'f', 'fatiguelife', 'fisk', 'foldcauchy', 'foldnorm', 'gamma', 'gausshyper', 'genexpon', 'genextreme', 'gengamma', 'genhalflogistic', 'genhyperbolic', 'geninvgauss', 'genlogistic', 'gennorm', 'genpareto', 'geom', 'gilbrat', 'gompertz', 'gumbel_l', 'gumbel_r', 'halfcauchy', 'halfgennorm', 'halflogistic', 'halfnorm', 'hypergeom', 'hypsecant', 'invgamma', 'invgauss', 'invweibull', 'johnsonsb', 'johnsonsu', 'kappa3', 'kappa4', 'ksone', 'kstwo', 'kstwobign', 'laplace', 'laplace_asymmetric', 'levy', 'levy_l', 'levy_stable', 'loggamma', 'logistic', 'loglaplace', 'lognorm', 'logser', 'loguniform', 'lomax', 'maxwell', 'mielke', 'moyal', 'nakagami', 'nbinom', 'ncf', 'nchypergeom_fisher', 'nchypergeom_wallenius', 'nct', 'ncx2', 'nhypergeom', 'norm', 'norminvgauss', 'pareto', 'pearson3', 'planck', 'poisson', 'powerlaw', 'powerlognorm', 'powernorm', 'randint', 'rayleigh', 'rdist', 'recipinvgauss', 'reciprocal', 'rice', 'semicircular', 'skellam', 'skewcauchy', 'skewnorm', 'studentized_range', 't', 'trapezoid', 'trapz', 'triang', 'truncexpon', 'truncnorm', 'tukeylambda', 'uniform', 'vonmises', 'vonmises_line', 'wald', 'weibull_max', 'weibull_min', 'wrapcauchy', 'yulesimon', 'zipf', 'zipfian']
```

<h4>Decision</h4>

```
decision <name>(<condition>, <decision event>) << <nation var> >>;
```


<h4>Function</h4>

```
function <name> << ... >>{
    #code
}
```

<h4>Events</h4>

```
#event for decision
decision event <name> (<category>) << <nation var> >>{
    #code
}

#event for simulation
simulation event <name>(<distribution>, <category>, <enable>, <decisions list>){
    #code
}
```

<h4>Func</h4>

```
#to begin the simulation
simulate(<time>);

#to get the value of an index
pos(<list>, <index>);

#to get the length of a list
len(<list>);

#to get the list of neighbors
neighbors(<nation>)

#to get the type
type(<value>);

#simulation
simulate(<total_time>);
simulate(<total_time>, <number_of_simulations>);


#plots
#property list
plot(<logs>, <nation>, <property list>, <graphic> );
#nation list
plot(<log>, <nations list>, <property>, <graphic>);
#data list
plot(logs->all, <nation>, <property>, 'dataframe');
graphic= ['line','bar','area']
log=[log1,log2,...] #number of the simulation carried out

```