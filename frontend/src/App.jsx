import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios';

function App() {
  const [count, setCount] = useState(0)

  function health() {
    axios.get(`http://88.217.37.253:7000/sample-app/health`)
    .then(response => {
      console.info(`sample-app /health endpoint response: `, response.data);
    })
    .catch(error => {
      console.log(error);
    });
  }

  const click1 = () => {
    console.info("test button clicked")
  }

  const exception = (num) => {
    const url = `http://88.217.37.253:7000/sample-app/exception${num}`
    console.info("excpetion handler() - url: ", url);
    axios.get(url)
    .then(response => {
      console.info(`sample-app /${exception} endpoint response: `, response.data);
    })
    .catch(error => {
      console.log(error);
    });

  }

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank" id="stransky">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React served by FastAPI - :-) </h1>
      <div className="card">
        <button onClick={() => { setCount((count) => count + 1); newrelic.addPageAction("count button clicked")} }>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p>
      <button onClick={health} >
          health call to backend
        </button>
        </p>
        <p>
      <button onClick={() => exception(1)} >
          backend: /excpetion1
        </button>
        </p>
        <p>
      <button onClick={() => exception(2)} >
          backend: /excpetion2
        </button>
        </p>
        <button onClick={click1} >
          test button
        </button>

      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
