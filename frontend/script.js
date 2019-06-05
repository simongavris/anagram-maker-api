const userAction = async () => {
  const response = await fetch('http://localhost:5000/api/get',
  {
    mode: 'no-cors',
    method: 'get'
  });
  const myJson = await response;//.json(); //extract JSON from the http response
  console.log(myJson);
  // do something with myJson
}
