a = {
     1: 'User : Durgesh.n',    2: '', 3: 'logo',
     4: 'Date : 12/12/2017',   5: 'logo',                  6: '',
     7: 'CameraName : CamXXX', 8: 'FocalLength : 60',           9: 'Frame : 1',
     10: 'aaaaaaaaaaaa',      11: 'bbbbbbbbbbbbbbbbbbbb',      12: ''
     }

for key, val in a.iteritems():
    if val == 'logo' or val.startswith('Frame :'):
        print key
        if key in [1, 2, 3, 7, 8, 9]:
            if not a[key + 3] == '':
                raise RuntimeError()
        if key in [4, 5, 6, 10, 11, 12]:
            if not a[key - 3] == '':
                raise RuntimeError()
