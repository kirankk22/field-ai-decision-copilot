function DetectionPanel({
  context,
  onClose,
  onAskAI,
}) {

  if (!context) {

    return (
      <div className="detection-panel empty">

        <h2>
          Field Detection
        </h2>

        <p>
          Select a detection on the map
          to view its details.
        </p>

      </div>
    );
  }


  const {
    detection,
    location,
    asset,
  } = context;


  return (

    <div className="detection-panel">


      <div className="panel-header">

        <div>

          <span className="panel-label">
            SELECTED DETECTION
          </span>

          <h2>
            {detection.id}
          </h2>

        </div>


        <button
          className="close-button"
          onClick={onClose}
        >
          ×
        </button>

      </div>


      <div className="detection-type">

        {detection.type}

      </div>


      <div className="status-row">

        <span
          className={
            `priority ${detection.priority.toLowerCase()}`
          }
        >

          {detection.priority}
          {" "}
          Priority

        </span>


        <span className="status">

          {detection.status}

        </span>

      </div>


      <div className="detection-details">


        <div className="detail">

          <span>
            Category
          </span>

          <strong>
            {detection.category}
          </strong>

        </div>


        <div className="detail">

          <span>
            Confidence
          </span>

          <strong>
            {
              (
                detection.confidence * 100
              ).toFixed(0)
            }%
          </strong>

        </div>


        <div className="detail">

          <span>
            Observed
          </span>

          <strong>
            {detection.observedDate}
          </strong>

        </div>


        <div className="detail">

          <span>
            District
          </span>

          <strong>
            {location.district}
          </strong>

        </div>


        <div className="detail">

          <span>
            Latitude
          </span>

          <strong>
            {location.latitude}
          </strong>

        </div>


        <div className="detail">

          <span>
            Longitude
          </span>

          <strong>
            {location.longitude}
          </strong>

        </div>


        <div className="detail">

          <span>
            Asset
          </span>

          <strong>
            {asset.id}
          </strong>

        </div>


      </div>


      <div className="description">

        <h3>
          Observation
        </h3>

        <p>
          {detection.description}
        </p>

      </div>


      <button
        className="ai-button"
        onClick={() => onAskAI(context)}
      >
        ✨ Ask AI Decision Copilot
      </button>


    </div>

  );
}


export default DetectionPanel;