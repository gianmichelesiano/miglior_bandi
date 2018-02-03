from firebase import firebase
firebase = firebase.FirebaseApplication('https://bandigare-8096d.firebaseio.com', None)
new_user = 'Ozgur Vatansever'

result = firebase.post('/users', new_user)
print result
