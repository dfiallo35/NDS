from compiler.execution import *


a= Code()
import time
t= time.time()
a.compile(
    '''
    category social();
    category economic();

    nation Cuba(10, 100, [], [], industrialization: 10 , economic_resources:100000, tourism:10, average_living_standard:10);
    nation USA(10, 100, [], [], industrialization: 100 , economic_resources:500000, tourism:90, average_living_standard:100);

    distribution pg(expon, scale: 10);
    distribution block(expon, scale: 50);


    decision event industrialization_increases(economic)<<n>>{
        n->economic_resources = n->economic_resources-5000;
        n->industrialization = n->industrialization*1.2;
    }    
    decision industrialization_increases_dec(n->economic_resources >= 5000, industrialization_increases)<< n >>;

    decision event tourism_increases(economic)<<n>>{
        n->economic_resources = n->economic_resources-7000;
        n->tourism = n->tourism*1.2;
    }
    decision tourism_increases_dec(n->economic_resources >= 7000, tourism_increases)<< n >>;

    decision event average_living_standard_increases(economic)<<n>>{
        n->economic_resources = n->economic_resources-3000;
        n->average_living_standard = n->average_living_standard*1.2;
    }    
    decision average_living_standard_increases_dec(n->economic_resources >= 3000, average_living_standard_increases)<< n >>;


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

    simulation event intensification_of_the_blockade(block,economic,true,[]){        
        foreach <<nat>> (map->nations){
            if nat == Cuba {
                nat->industrialization=nat->industrialization*0.9;
                nat->tourism=nat->average_living_standard*0.9;
                nat->average_living_standard=nat->average_living_standard*0.9;
            }
        }
    }

    simulation event population_mortality(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= nat->population - irvs(expon, loc: 0);
        }
    }

    simulate(50d);


    '''
)
print('>>>>>', time.time()-t)