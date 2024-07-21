from .models import db, Application, Grimorio
import random

# Un trébol de una o dos hojas es común, uno de tres es poco habitual, 
# uno de cuatro es inusual, y uno de cinco hojas muy raro.
CLOVERS = {
    'Trébol una hoja': 4,
    'Trébol dos hojas': 3,
    'Trébol tres hojas': 2,
    'Trébol cuatro hojas': 1,
    'Trébol cinco hojas': 0.5
}

def assign_grimorio(application):
    """
        Asigna un Grimorio a una solicitud de magia
    """
    print('assign')
    clover_types = list(CLOVERS.keys())
    ponderaciones = list(CLOVERS.values())
    
    assigned_type = random.choices(clover_types, weights=ponderaciones, k=1)[0]

    grimorio = Grimorio(clover_type=assigned_type, rarity=assigned_type, assignment=application.identity)
    db.session.add(grimorio)
    db.session.commit()
    return f'{assigned_type}'

