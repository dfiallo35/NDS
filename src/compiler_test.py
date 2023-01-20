from compiler.execution import *


a= Code()
a.compile(
    '''
    category social();
    category economic();

    nation Cuba(10, 100, [], [], industrialization: 10 , economic_resources:30000);
    nation USA(10, 100, [], [], industrialization: 10 , economic_resources:30000);

    distribution pg(expon, scale: 4);

    decision event industrialization_increases(economic)<<n>>{
        n->economic_resources=n->economic_resources-5000;
        n->industrialization=n->industrialization*0.9;
    }

    decision industrialization_increases_dec(n->economic_resources>=5000, industrialization_increases)<< n >>;

    simulation event population_growth(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= irvs(expon, loc: nat->population);
        }
    }

    simulation event decrease_industrialization(pg,economic,true,[]){
        foreach <<nat>> (map->nations){
            nat->industrialization=nat->industrialization*0.9;
        }
    }

    simulation event population_mortality(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= nat->population - irvs(expon, loc: 0);
        }
    }

    simulate(100d);


    '''
)