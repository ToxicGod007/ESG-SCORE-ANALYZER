import React, { useEffect, useState } from 'react';

// ... inside the component ...
const [apiData, setApiData] = useState(null);

useEffect(() => {
  fetch('http://localhost:8000/api/esg-score')
    .then(res => res.json())
    .then(data => setApiData(data));
}, []);