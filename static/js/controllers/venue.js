export function addNewVenue (e) {
  e.preventDefault();
  console.log(e,'submit')

  const newVenue = {
    'name': document.getElementById('name').value,
    'city': document.getElementById('city').value,
    'state': document.getElementById('state').value,
    'address': document.getElementById('address').value,
    'phone': document.getElementById('phone').value,
    'genres': document.getElementById('genres').value,
    'imageLink': document.getElementById('image_link').value,
    'facebookLink': document.getElementById('facebook_link').value,
    'websiteLink': document.getElementById('website_link').value,
    'seekingTalent': document.getElementById('seeking_talent').value,
    'seekingDescription': document.getElementById('seeking_description').value
  }

  console.log('new-venue:', newVenue)
  fetch('/venues/create', {
    method: 'POST',
    body: JSON.stringify(newVenue),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function(response) {
    console.log('html', response.url)
    window.location.href = response.url;
  })
  .catch(function() {
    console.log('error in fetch');
  })
}

export function updateVenue (e) {
  e.preventDefault();
  const venueId = document.querySelector('.form-heading').dataset['id'];
  console.log(e,'submit', venueId)

  const updatedVenue = {
    'name': document.getElementById('name').value,
    'city': document.getElementById('city').value,
    'state': document.getElementById('state').value,
    'address': document.getElementById('address').value,
    'phone': document.getElementById('phone').value,
    'genres': document.getElementById('genres').value,
    'imageLink': document.getElementById('image_link').value,
    'facebookLink': document.getElementById('facebook_link').value,
    'websiteLink': document.getElementById('website_link').value,
    'seekingTalent': document.getElementById('seeking_talent').value,
    'seekingDescription': document.getElementById('seeking_description').value
  }

  console.log('new-venue:', updatedVenue)
  fetch(`/venues/${venueId}/edit`, {
    method: 'POST',
    body: JSON.stringify(updatedVenue),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function(response) {
    console.log('html', response.url)
    window.location.href = response.url;
  })
  .catch(function() {
    console.log('error in fetch');
  })
}

