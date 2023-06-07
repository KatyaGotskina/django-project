MIN_LN_LEN = 4
UNSAFE_METHODS = 'POST', 'PUT', 'DELETE'

#choices for models
ORDER_STATUSES = (
        ('canceled', 'canceled'),
        ('completed', 'completed'),
        ('created', 'created'), 
        ('in_basket', 'in_basket')
)
PR_STATUS = (
    ('for sale', 'for sale'),
    ('removed', 'removed'),
)