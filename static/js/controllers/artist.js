export function addNewArtist (e) {
  e.preventDefault();
  console.log(e,'submit')

  const newArtist = {
    'name': document.getElementById('name').value,
    'city': document.getElementById('city').value,
    'state': document.getElementById('state').value,
    'phone': document.getElementById('phone').value,
    'genres': document.getElementById('genres').value,
    'imageLink': document.getElementById('image_link').value,
    'facebookLink': document.getElementById('facebook_link').value,
    'websiteLink': document.getElementById('website_link').value,
    'seekingVenue': document.getElementById('seeking_venue').value,
    'seekingDescription': document.getElementById('seeking_description').value
  }

  console.log('new-artist:', newArtist)
  fetch('/artists/create', {
    method: 'POST',
    body: JSON.stringify(newArtist),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function(response) {
    console.log('html', response.url)
    window.location.href = response.url;
    // return response.json();
  })
  // .then(function(jsonResponse) {
  //   console.log('html', jsonResponse.url)
  //   window.location.href = jsonResponse.url;
  // })
  .catch(function() {
    console.log('error in fetch');
  })
}

export function updateArtist (e) {
  e.preventDefault();
  const artistId = document.querySelector('.form-heading').dataset['id'];

  console.log(e,'submit edit',artistId)


  const updatedArtist = {
    'name': document.getElementById('name').value,
    'city': document.getElementById('city').value,
    'state': document.getElementById('state').value,
    'phone': document.getElementById('phone').value,
    'genres': document.getElementById('genres').value,
    'imageLink': document.getElementById('image_link').value,
    'facebookLink': document.getElementById('facebook_link').value,
    'websiteLink': document.getElementById('website_link').value,
    'seekingVenue': document.getElementById('seeking_venue').value,
    'seekingDescription': document.getElementById('seeking_description').value
  }

  console.log('updated-artist:', updatedArtist)
  fetch(`/artists/${artistId}/edit`, {
    method: 'POST',
    body: JSON.stringify(updatedArtist),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function(response) {
    console.log('html', response.url)
    window.location.href = response.url;
    // return response.json();
  })
  // // .then(function(jsonResponse) {
  // //   console.log('html', jsonResponse.url)
  // //   window.location.href = jsonResponse.url;
  // // })
  .catch(function() {
    console.log('error in fetch');
  })
}

