import {
  useEffect,
  useRef,
  useState,
} from "react";

import MapView from "./components/MapView";
import DetectionPanel from "./components/DetectionPanel";
import AICopilot from "./components/AICopilot";

import "./index.css";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL;


if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not configured."
  );
}


function App() {

  const [
    detections,
    setDetections,
  ] = useState([]);


  const [
    selectedDetection,
    setSelectedDetection,
  ] = useState(null);


  const [
    aiContext,
    setAiContext,
  ] = useState(null);


  const [
    loading,
    setLoading,
  ] = useState(true);


  const [
    error,
    setError,
  ] = useState(null);


  // --------------------------------------------------
  // Keep track of the latest detection request.
  //
  // This prevents an older request from DET-001
  // overwriting a newer selection such as DET-002.
  // --------------------------------------------------

  const detectionRequestId =
    useRef(0);


  // ==================================================
  // LOAD DETECTIONS
  // ==================================================

  useEffect(() => {

    const loadDetections =
      async () => {

        try {

          setLoading(true);

          const response =
            await fetch(
              `${API_BASE_URL}/api/detections`
            );


          if (!response.ok) {

            throw new Error(
              "Failed to load detections"
            );

          }


          const data =
            await response.json();


          setDetections(data);

        } catch (err) {

          console.error(err);

          setError(
            "Unable to load detections."
          );

        } finally {

          setLoading(false);

        }

      };


    loadDetections();

  }, []);


  // ==================================================
  // DETECTION SELECTION
  // ==================================================

  const handleDetectionSelect =
    async (detection) => {

      // ------------------------------------------------
      // Every new map selection starts a new request.
      // ------------------------------------------------

      detectionRequestId.current += 1;

      const currentRequestId =
        detectionRequestId.current;


      console.log(
        "Selected detection:",
        detection.id
      );


      // ------------------------------------------------
      // IMPORTANT:
      //
      // Close/reset the AI Copilot immediately when
      // another detection is selected.
      //
      // This prevents DET-001 conversation/context
      // from remaining active while DET-002 loads.
      // ------------------------------------------------

      setAiContext(null);


      // ------------------------------------------------
      // Load the new detection context.
      // ------------------------------------------------

      try {

        const response =
          await fetch(
            `${API_BASE_URL}/api/detections/${detection.id}/context`
          );


        if (!response.ok) {

          throw new Error(
            "Failed to load detection context"
          );

        }


        const context =
          await response.json();


        // ------------------------------------------------
        // Ignore stale responses.
        //
        // Example:
        //
        // DET-001 request starts
        // DET-002 request starts
        // DET-002 finishes
        // DET-001 finishes later
        //
        // DET-001 must NOT overwrite DET-002.
        // ------------------------------------------------

        if (
          currentRequestId !==
          detectionRequestId.current
        ) {

          return;

        }


        console.log(
          "Detection context:",
          context
        );


        setSelectedDetection(
          context
        );


      } catch (error) {

        console.error(
          "Detection context error:",
          error
        );


        // Do not overwrite the currently selected
        // detection if this request is stale.

        if (
          currentRequestId ===
          detectionRequestId.current
        ) {

          setError(
            "Unable to load detection details."
          );

        }

      }

    };


  // ==================================================
  // CLOSE DETECTION PANEL
  // ==================================================

  const handleClosePanel =
    () => {

      setSelectedDetection(null);

      setAiContext(null);

    };


  // ==================================================
  // OPEN AI COPILOT
  // ==================================================

  const handleAskAI =
    (context) => {

      console.log(
        "AI Decision Copilot context:",
        context
      );


      setAiContext(
        context
      );

    };


  // ==================================================
  // CLOSE AI COPILOT
  // ==================================================

  const handleCloseAI =
    () => {

      setAiContext(null);

    };


  // ==================================================
  // RENDER
  // ==================================================

  return (

    <div className="app">

      {/* ==============================================
          TOP BAR
          ============================================== */}

      <header className="top-bar">

        <div className="logo">
          Field AI Intelligence
        </div>


        <div className="top-menu">

          <span>
            Map
          </span>

          <span>
            Detections
          </span>

          <span>
            Assets
          </span>

          <span>
            Reports
          </span>

        </div>

      </header>


      {/* ==============================================
          MAIN LAYOUT
          ============================================== */}

      <main className="main-content">


        {/* ============================================
            SIDEBAR
            ============================================ */}

        <aside className="sidebar">

          <h3>
            Filters
          </h3>


          <div className="filter-section">

            <label>
              Client
            </label>

            <select>

              <option>
                Demo Municipal Corporation
              </option>

            </select>

          </div>


          <div className="filter-section">

            <label>
              District
            </label>

            <select>

              <option>
                District 3
              </option>

            </select>

          </div>


          <div className="filter-section">

            <label>
              Detection Types
            </label>


            <label className="checkbox">

              <input
                type="checkbox"
                defaultChecked
              />

              Road Safety

            </label>


            <label className="checkbox">

              <input
                type="checkbox"
                defaultChecked
              />

              Infrastructure

            </label>


            <label className="checkbox">

              <input
                type="checkbox"
                defaultChecked
              />

              Vegetation

            </label>


            <label className="checkbox">

              <input
                type="checkbox"
                defaultChecked
              />

              Lighting

            </label>

          </div>

        </aside>


        {/* ============================================
            MAP
            ============================================ */}

        <section className="map-section">

          {loading && (

            <div
              style={{
                padding: "20px",
                position: "absolute",
                zIndex: 1000,
                background: "white",
              }}
            >

              Loading detections...

            </div>

          )}


          {error && (

            <div
              style={{
                padding: "20px",
                position: "absolute",
                zIndex: 1000,
                background: "#ffe1df",
                color: "#b42318",
              }}
            >

              {error}

            </div>

          )}


          {!loading &&
            !error && (

              <MapView
                detections={
                  detections
                }
                onDetectionSelect={
                  handleDetectionSelect
                }
              />

            )}

        </section>


        {/* ============================================
            DETECTION DETAILS
            ============================================ */}

        <aside className="details-section">

          <DetectionPanel
            context={
              selectedDetection
            }
            onClose={
              handleClosePanel
            }
            onAskAI={
              handleAskAI
            }
          />

        </aside>

      </main>


      {/* ==============================================
          AI DECISION COPILOT
          ============================================== */}

      <AICopilot
        key={
          aiContext?.detection?.id ||
          "no-detection"
        }
        context={
          aiContext
        }
        onClose={
          handleCloseAI
        }
      />

    </div>

  );

}


export default App;
