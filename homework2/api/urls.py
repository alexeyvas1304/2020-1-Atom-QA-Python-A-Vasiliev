CONTINUE_URL = 'https://target.my.com/auth/mycom?state=target_login%3D1#email'
FAILURE_URL = 'https://account.my.com/login/'
AUTH_URL = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'
CSRF_URL = 'https://target.my.com/csrf/'
CREATE_SEGMENT_URL = 'https://target.my.com/api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations_count,id,name,pass_condition,created,campaign_ids,users,flags'
DELETE_SEGMENT_URL = 'https://target.my.com/api/v2/remarketing/segments/{}.json'