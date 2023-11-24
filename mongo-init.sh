set -e

mongosh <<EOF
db = db.getSiblingDB('memo')
db.createCollection('user')

userCol = db.getCollection('user')

userCol.insert([
    {"name":"Albertus","status":"patient","age": 25,"memory_score": 10,"password":"sha256\$lJHVtdx2GNjtbCNN\$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
    {"name":"Violetta","status":"caregiver","related_patients":[],"password":"sha256\$lJHVtdx2GNjtbCNN\$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
    {"name":"Markus","status":"healthcare_professionnal","type":"general_practitionner","password":"sha256\$lJHVtdx2GNjtbCNN\$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
    {"name":"Marta","status":"healthcare_professionnal","type":"neurologist","password":"sha256\$lJHVtdx2GNjtbCNN\$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
    {"name":"Iga","status":"healthcare_professionnal","type":"psychologist","password":"sha256\$lJHVtdx2GNjtbCNN\$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"}
])

EOF