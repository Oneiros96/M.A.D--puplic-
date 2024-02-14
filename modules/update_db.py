def update_db(updates, db):
    for update in updates:
        parameters = []
        # If Entry alredy exists
        if db.execute("Select * FROM offers WHERE offer_id = ?",(update['offer_id'],)):
            query = "UPDATE offers SET "

            offer_id = update.pop("offer_id") #saves the offer id in the variable and deletes it from the update dict
            for index, (key, value) in enumerate(update.items(), start=1):
                query += f"{key} = ?"
                parameters.append(value)
                if index != len(update):
                    query += ", "
            query += " WHERE offer_id = ?"
            parameters.append(offer_id)
        # If it is an new entry
        else:
            del update["offer_id"]
            query = "INSERT INTO offers ("
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