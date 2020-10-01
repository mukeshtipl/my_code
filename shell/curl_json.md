Setup a mock API server for request test

When we build an API-based web (front-end and back-end separated), we usually want to see what the HTTP client is sending or to inspect and debug webhook requests. There are two approaches:

    Build an API server by ourselves
    Use a fake mock API server

In this post, we choose the second approach and use RequestBin.

Three ways to pass the environment variables
1 Add a single quote and a double quote around the variable

$ curl -X POST https://requestbin.io/1bk0un41  -H "Content-Type: application/json" -d '{ "property1":"'"$TERM"'", "property2":"value2" }'

We can see the result is what we want.
Image for post
Image for post
2 Escaping double quote

The Outermost layer uses double-quotes. And add escaping mark for each double quote in the JSON data part.

$ curl -X POST https://requestbin.io/1bk0un41 -H "Content-Type: application/json" -d "{ \"property1\":\"$TERM\", \"property2\":\"value2\" }"

3 Use a data generation function

This method can save us from all sort of headaches concerning shell quoting and makes it easier to read and maintain.

generate_post_data()
{
cat <<EOF
{
"property1":"\$TERM",
"property2":"value2"
}
EOF
}

Add the function to curl:

$ curl -X POST https://requestbin.io/1bk0un41 -H "Content-Type: application/json" -d "$(generate_post_data)"

Image for post
