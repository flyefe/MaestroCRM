import MySQLdb

db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='',
    db='djangocrm',
    ssl={'ca': '', 'cert': '', 'key': ''}
)

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version : %s " % data)
db.close()


conditions = [
    {
        "type": "status",
        "operation": "=",
        "value": "active",
        "logic": "and"
    },
    {
        "type": "tag",
        "operation": "!=",
        "value": "urgent",
        "logic": "or"
    }
]

# Initialize the main Q object
q = Q()

# Variable to keep track of the current condition
current_q = None

for i, condition in enumerate(conditions):
    # Create a new Q object for each condition
    new_q = Q()
    
    if condition['type'] == 'status':
        if condition['operation'] == '=':
            new_q &= Q(status=condition['value'])
        elif condition['operation'] == '!=':
            new_q &= ~Q(status=condition['value'])
    elif condition['type'] == 'tag':
        if condition['operation'] == '=':
            new_q &= Q(tags__name=condition['value'])
        elif condition['operation'] == '!=':
            new_q &= ~Q(tags__name=condition['value'])
    
    # Logic for combining conditions
    if i == 0:
        # For the first condition, just set it as the current condition
        current_q = new_q
    else:
        # Combine with the previous condition based on the logic
        if condition['logic'] == 'and':
            current_q &= new_q
        elif condition['logic'] == 'or':
            current_q |= new_q

# After the loop, current_q holds the combined query
q = current_q

# Now you can use q to filter your contacts
contacts = Contact.objects.filter(q)




conditions = [
    {
        "type": "status",
        "operation": "=",
        "value": "active",
        "logic": "or"
    },
    {
        "type": "tag",
        "operation": "!=",
        "value": "urgent",
        "logic": "and"
    }
    {
        "type": "tag",
        "operation": "=",
        "value": "good",
        "logic": "or"
    }
    {
        "type": "age",
        "operation": ">",
        "value": "20",
        "logic": "or"
    }
    {
        "type": "published_date",
        "operation": "=",
        "value": "2023",
        "logic": "and"
    }
    {
        "type": "tag",
        "operation": "!=",
        "value": "game",
        "logic": "or"
    }
    {
        "type": "status",
        "operation": "!=",
        "value": "closed",
        "logic": "or"
    }
]

q = (
    Q(status="active") | 
    (~Q(tags__name="urgent") & (Q(tags__name="good")) | 
    (Q(age__gt=20) &  (Q(published_date=2023)) | 
    (~Q(tags__name="game") | (~Q(status="closed")))
    ))
)