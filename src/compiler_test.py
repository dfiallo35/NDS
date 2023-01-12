from compiler.execution import *


a= Code()
a.compile(
    '''
    re=1;

    
    # event fib <<n: number>>{
    #     if(n == 0){
    #         return 0;
    #     }
    #     if(n == 1){
    #         return 1;
    #     }
    #     else{
    #         return fib(n-1) + fib(n-2);
    #     }
    # }
    # show(fib(10));


    # show(params(event));
    # show(1 == 4);

    # category socialism();
    # category capitalism();

    # province Havana(100, 10, 10345);
    # province Mayabeque(236, 10, 204);
    # province New_York(2056, 20, 103856);
    # province California(341, 30, 402175);

    # nation Cuba([Havana, Mayabeque], [socialism]);
    # nation USA([New_York, California], [capitalism]);
    
    # distribution pg(expon, scale: 4);

    # show(pos(Cuba->provinces, 0)->extension);
    # pos(Cuba->provinces, 0) -> extension: 200;
    # show(pos(Cuba->provinces, 0)->extension);

    # event population_growth(pg, socialism, true, []){
    #     for(prov, map->provinces){
    #         prov->population: irvs(expon, loc: prov->population);
    #     }
    # }

    # event population_mortality(pg, socialism, true, []){
    #     for(prov, map->provinces){
    #         prov->population: prov->population - irvs(expon, loc: 0);
    #     }
    # }

    # simulate(100d);

    # nation Cuba([Mayabeque], [crazy]);
    # Cuba->provinces: ++Havana;
    # Cuba->provinces: --Mayabeque;
    # show(Cuba->provinces);

    

    # decision a(n==1, fib)<< n >>;

    '''
)
# print(a.map.decisions['a'].condition(1))
# print('map', a.elements)
# print('vars', a.vars)
# print('events', a.events)