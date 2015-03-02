openssl x509 -purpose -in CA.cert  -inform  PEM

openssl x509 -purpose -in servercert.csr  -inform  PEM

openssl req  -newkey rsa:2048 -sha256 -nodes -out servercert.csr -outform PEM

openssl req  -text  -noout -verify -in servercert.csr

openssl ca -config openssl.cnf -policy signing_policy -extensions signing_req -out servercert.pem -infiles servercert.csr




