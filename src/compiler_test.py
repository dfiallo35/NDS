from compiler.execution import *


a= Code()
import time
t= time.time()
a.compile(
    '''
    #categories
    category social();
    category economic();
    category political();
    category military();
    category territorial();

    #nations
    nation Cuba(11256372, 109884 , [], [],aviable_economic_resources:112000, industrialization: 30 , PIB:  45510000000, tourism:80, average_living_standard:50, life_expectancy: 75,employment: 97.2);
    nation USA(9147593, 337341954, [], [],aviable_economic_resources:834500000, industrialization: 80 , PIB:15700000000000000, tourism:70, average_living_standard:75,life_expectancy: 77,employment: 94.5);
    nation Canada(38246108, 9984670, [], [],aviable_economic_resources:53120000, industrialization: 70 , PIB:2027371000000, tourism:30, average_living_standard:80,life_expectancy: 82,employment: 98.5);
    nation Mexico(128455567, 1964375 , [], [],aviable_economic_resources:93410000, industrialization: 60 , PIB:2890685000000, tourism:70, average_living_standard:68,life_expectancy: 70,employment: 94.9);


    #distributions
    distribution pg(expon, scale: 20);
    distribution block(expon, scale: 50);



    #decisions
    decision event industrialization_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-500;
        n->industrialization = n->industrialization*1.2;
    }    
    decision industrialization_increases_dec(n->aviable_economic_resources >= 5000, industrialization_increases)<< n >>;

    decision event tourism_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-7000;
        n->tourism = n->tourism*1.2;
    }
    decision tourism_increases_dec(n->aviable_economic_resources >= 7000, tourism_increases)<< n >>;

    decision event average_living_standard_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-6000;
        n->life_expectancy= n->life_expectancy*1.2;
        n->average_living_standard = n->average_living_standard*1.2;
    }    
    decision average_living_standard_increases_dec(n->aviable_economic_resources >= 6000, average_living_standard_increases)<< n >>;

    decision event create_jobs(social)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-4000;
        n->employment = n->employment*1.2;
    }
    decision create_jobs_dec(n->aviable_economic_resources >= 4000, create_jobs)<< n >>;

    # decision event increment_aviable_economic_resources(social)<<n>>{
    #     a = n->PIB * 0.1;
    #     n->PIB = n->PIB - a;
    #     n->aviable_economic_resources = n->aviable_economic_resources + a;
    # }    
    # # decision increment_aviable_economic_resources_dec(n->PIB >= n->population*100, increment_aviable_economic_resources)<< n >>;



    #events

    simulation event unemployment_increases(pg, social, true, []){
        foreach <<nat>> (map->nations){
        nat->employment= nat->employment*0.9;
        nat->average_living_standard= nat->average_living_standard*0.9;
        }
    }

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


    foreach <<nat>> (map->nations){
        show(nat,nat->tourism);
    }


    simulate(10d);

    plot(Cuba, ['tourism', 'industrialization'] , 'line');


    foreach <<nat>> (map->nations){
        show(nat,nat->tourism);
    }


    '''
)
print('>>>>>', time.time()-t)