from compiler.execution import *


a= Code()
a.compile(
    '''
    category socialism();
    category capitalism();

    nation Cuba(10, 100, [], [], pollo: 10);
    nation USA(10, 100, [], []);

    distribution pg(expon, scale: 4);

    decision event a (socialism)<<n>>{
        show(n);
    }

    simulation event population_growth(pg, socialism, true, []){
        foreach <<nat>> (map->nations){
            nat->population= irvs(expon, loc: nat->population);
        }
    }

    simulation event population_mortality(pg, socialism, true, []){
        foreach <<nat>> (map->nations){
            nat->population= nat->population - irvs(expon, loc: 0);
        }
    }

    simulate(100d);

    # decision a(n==1, a)<< n >>;

    '''
)