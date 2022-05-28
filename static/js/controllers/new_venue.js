export function logString (e) {
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
    // const newUrl = response.json().url
    console.log('html', response.url)
    // return response.json();
    // window.location = newUrl
    window.location.href = response.url;
    // return response.json();
  })
  // .then(function(jsonResponse) {
  //   console.log(jsonResponse);
    // const liItem = document.createElement('li');
    // const linkItem = document.createElement('a');

    // const checkbox = document.createElement('input');
    // checkbox.className = 'check-list';
    // checkbox.type = 'checkbox';
    // checkbox.setAttribute('data-id', jsonResponse.id);
    // liItem.appendChild(checkbox);

    // const text = document.createTextNode(' ' + jsonResponse.name);
    // const id = jsonResponse.id;
    // console.log(id, 'id')
    // linkItem.appendChild(text);
    // linkItem.setAttribute('href', `/lists/${id}`);
    // liItem.appendChild(linkItem);

    // const deleteBtn = document.createElement('button');
    // deleteBtn.className = 'delete-list';
    // deleteBtn.setAttribute('data-id', jsonResponse.id);
    // deleteBtn.innerHTML = '&cross;';
    // liItem.appendChild(deleteBtn);

    // document.getElementById('todo-lists').appendChild(liItem);
    // document.getElementById('list-error').classname='hidden';
  // })
  .catch(function() {
    console.log('error in fetch');
  })
}

