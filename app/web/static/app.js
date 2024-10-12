document
  .getElementById("url-entry-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // prevents page refresh on submit

    const urlEntry = document.getElementById("url-entry").value;
    console.info(urlEntry);

    axios
      .post("/process_url", { url: urlEntry })
      .then(function (response) {
        if (response.data.success) {
          console.log(response.data.details.title);
          console.log(response.data.streams);

          document.getElementById("video-title").textContent =
            response.data.details.title;
          document.getElementById("wrong-url-message").style.display = "none";
          document.getElementById("processing-message").style.display = "none";
          document.getElementById("download-link").style.display = "none";
          document.getElementById("start-download").style.display = "block";

          const streams = response.data.streams;
          const streamsDropdown = document.getElementById("available-streams");
          streamsDropdown.innerHTML = "";

          Object.keys(streams).forEach(function (key) {
            const option = document.createElement("option");
            option.text = key;
            option.value = streams[key];
            streamsDropdown.appendChild(option);
          });

          document.getElementById("video-download-part").style.display =
            "block";
        }
      })
      .catch(function (error) {
        if (error.response) {
          const errorMessageDiv = document.getElementById("wrong-url-message");
          errorMessageDiv.textContent =
            "Wrong link! Please correct it and try again.";
          errorMessageDiv.style.display = "block";
          document.getElementById("video-download-part").style.display = "none";
        } else {
          console.error("Error: ", error.message);
        }
      });
  });

document
  .getElementById("start-download")
  .addEventListener("click", function (event) {
    document.getElementById("start-download").style.display = "none";
    document.getElementById("processing-message").style.display = "block";

    const selectedStreamId = document.getElementById("available-streams").value;

    axios
      .post("/start_download", { stream_id: selectedStreamId })
      .then((response) => {
        const queueId = response.data.queue_id;

        const checkStatus = setInterval(() => {
          axios.get(`/check_download_status/${queueId}`).then((res) => {
            if (res.data.status == "completed") {
              clearInterval(checkStatus);
              document.getElementById("processing-message").style.display =
                "none";
              console.log(res.data.download_url);
              document.getElementById("download-link").style.display = "block";
              document
                .getElementById("download-link")
                .querySelector("a")
                .setAttribute("href", res.data.download_url);
            }
          });
        }, 3000);
      })
      .catch((error) => {
        console.error(error);
        document.getElementById("processing-message").innerHTML =
          "Error during download";
        document.getElementById("start-download").style.display = "block";
      });
  });
