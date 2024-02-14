def save_customer(customer, db):
    ###############################################
    # Checks if a customer exists in the database #
    # and add's it if not                         #
    ###############################################
    if not db.execute("SELECT * FROM customers WHERE name = ?", (customer["name"],)):
        db.execute("INSERT INTO customers (name, street, street_nr, postal_code, city) VALUES(?, ?, ?, ?, ?)",
                   (customer["name"], customer["street"], customer["street_nr"], customer["postal_code"], customer["city"]))
        
def update_customers(updates, db):
    for update in updates:
        parameters = []
        # If Entry alredy exists
        if db.execute("Select * FROM customers WHERE customer_id = ?",(update['customer_id'],)):
            query = "UPDATE customers SET "

            customer_id = update.pop("customer_id") #saves the offer id in the variable and deletes it from the update dict
            for index, (key, value) in enumerate(update.items(), start=1):
                query += f"{key} = ?"
                parameters.append(value)
                if index != len(update):
                    query += ", "
            query += " WHERE customer_id = ?"
            parameters.append(customer_id)
        # If it is an new entry
        else:
            del update["customer_id"]
            query = "INSERT INTO customers ("
            for key in update.keys():
                query += f"{key}, "
            query = query[:-2]
            query += ") Values ("
            for value in update.values():
                query += f"?, "
                parameters.append(value)
            query = query[:-2]
            query += ")"
        db.execute(query, parameters)