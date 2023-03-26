from bs4 import BeautifulSoup


def read_resp(fname):
    file_new_html = open(fname, 'r', encoding='utf-8')
    ss_new = file_new_html.read()
    file_new_html.close()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(ss_new, 'html.parser')

    # Find the table element in the HTML
    table = soup.find('table')

    # Find all rows in the table
    rows = table.find_all('tr')

    # Loop through each row and extract the data from the columns
    data = []
    for row in rows:
        if row.has_attr('id') and row['id'].startswith('tr_'):
            columns = row.find_all('td')
            row_data = []
            for column in columns:
                if column.find('a') is not None:
                    # If the column contains an <a> tag, get the href attribute value
                    row_data.append(column.find('a')['href'])
                else:
                    # Otherwise, just get the text content of the column
                    row_data.append(column.text.strip())
            data.append(row_data)
    return data


def compare_resp(fname_old, fname_new):
    data_old = read_resp(fname_old)
    data_new = read_resp(fname_new)

    print("Compare resp data: ")
    print(data_old)
    print(data_new)

    old_set = set(tuple(row) for row in data_old)
    new_set = set(tuple(row) for row in data_new)
    diff_set = new_set - old_set
    diff_list = [list(row) for row in diff_set]
    return diff_list


def overwrite_old_resp(fname_old, fname_new):
    print("Overwriting file " + fname_old)
    with open(fname_old, 'w', encoding='utf-8') as f_old, open(fname_new, 'r', encoding='utf-8') as f_new:
        f_new_content = f_new.read()
        f_old.write(f_new_content)
    f_old.close()
    f_new.close()


def resp_handler(advert):
    if advert == "added":
        print("Found new advertisement!")
        return 1
    if advert == "none":
        print("No new advertisements added! No notifications will be sent")
        return 0
    if advert == "removed":
        print("An advertisement has been removed!")
        return 1
    print("Something went horribly wrong...")
    return 0


def format_resp(diff_data):
    counter = 0
    while len(diff_data) > counter:
        if counter == 0:
            email_payload = "Advertisement link: https://www.ss.com" + diff_data[counter][2] + "\n"
        else:
            email_payload += "Advertisement link: https://www.ss.com" + diff_data[counter][2] + "\n"
        email_payload += "Street: " + diff_data[counter][3] + "\n"
        email_payload += "Room count: " + diff_data[counter][4] + "\n"
        email_payload += "Area: " + diff_data[counter][5] + " m2\n"
        email_payload += "Floor: " + diff_data[counter][6] + "\n"
        email_payload += "House model: " + diff_data[counter][7] + "\n"
        email_payload += "Price for m2: " + diff_data[counter][8] + "\n"
        email_payload += "Total price: " + diff_data[counter][9] + "\n"
        email_payload += "================================\n\n"
        counter += 1
    print("Advertisement count added to email: ", counter)
    return email_payload
