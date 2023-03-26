import get_response
import read_response
# import send_email

# Define file names where data will be stored
fname_old = "SS_response_old.html"
fname_new = "SS_response_new.html"

# Define request url - can change locations - centre, other cities etc.
request_url = "https://www.ss.com/lv/real-estate/flats/riga/centre/sell/filter/"
# request_url = "https://www.ss.com/lv/real-estate/flats/riga/maskavas-priekshpilseta/sell/"

# Set up filter parameters for the filter request:
# topt[8]: min/max price
# topt[1]: min/max room count
# topt[3]: min/max area in
# topt[4]: min/max floor
# opt[6]: house series
# sid: service ID
# opt[11]: street (?)
filter_conds = {
    'topt[8][min]': '',
    'topt[8][max]': '120000',
    'topt[1][min]': '2',
    'topt[1][max]': '',
    'topt[3][min]': '46',
    'topt[3][max]': '',
    'topt[4][min]': '2',
    'topt[4][max]': '',
    'opt[6]': '',
    'sid': '/lv/real-estate/flats/riga/centre/sell/filter/',
    'opt[11]': ''
}

# Gets html response
get_response.get_ss_resp(filter_conds, request_url, fname_old, fname_new)

# Compare old to new
diff_data = read_response.compare_resp(fname_old, fname_new)

# Compare new to old
if len(diff_data) == 0:
    diff_data = read_response.compare_resp(fname_new, fname_old)
    if len(diff_data) == 0:
        send_notifs = read_response.resp_handler("none")
    else:
        send_notifs = read_response.resp_handler("removed")
else:
    send_notifs = read_response.resp_handler("added")

if send_notifs == 1:
    read_response.overwrite_old_resp(fname_old, fname_new)
    print(diff_data)
    email_payload = read_response.format_resp(diff_data)
    print(email_payload)
    # send email_payload to email
else:
    print("Nothing to be done. End program.")

# email send - NOT FINISHED
