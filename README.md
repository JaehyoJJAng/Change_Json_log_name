# Parameko 라이브러리 사용하여 JSON log 파일명 변경하기

# 요구사항

**변경할 파일명**
- `20230324_13_54_http_0.json`
- `20230324_13_54_netapps_0.json`

**변경될 파일명**
- `20230324-http-001.json`
- `20230324-netapps-001.json`

`http` 와 `netapps` 구분하여 파일명 변경하고 변경안된 파일명들 기준으로 시퀀스 넘버처리 하는데
뒤에 0채워서 변경 하도록 함
