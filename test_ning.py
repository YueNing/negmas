import random
random.seed(0)
from pprint import pprint
from negmas import SAOMechanism, AspirationNegotiator, MappingUtilityFunction, SAOProtocol
from negmas import Issue, SAOMechanism, AspirationNegotiator, normalize
from negmas.utilities import LinearUtilityAggregationFunction as LUFun
issues = [Issue(name='price', values=10), Issue(name='quantity', values=10)
          , Issue(name='delivery_time', values=10)]

session = SAOMechanism(issues=issues, n_steps=2000)

buyer_utility = normalize(ufun=LUFun(issue_utilities={'price': lambda x: 9.0 - x
                                       , 'quantity': lambda x: 0.2 * x
                                       , 'delivery_time': lambda x: x})
                         , outcomes=session.outcomes)

seller_utility = normalize(ufun=LUFun(issue_utilities={'price': lambda x: x
                                       , 'quantity': lambda x: 0.2 * x
                                       , 'delivery_time': lambda x: 9.0 - x})
                           , outcomes=session.outcomes)


session.add(AspirationNegotiator(name='buyer'), ufun=buyer_utility)
session.add(AspirationNegotiator(name='seller'), ufun=seller_utility)

pprint(session.run().__dict__)
session.plot(plot_outcomes=False)