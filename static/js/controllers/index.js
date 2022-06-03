
import { addNewVenue, updateVenue } from './venue.js';
import { addNewArtist, updateArtist } from './artist.js';

if (document.getElementById('venue-form')) {
  document.getElementById('venue-form').onsubmit = addNewVenue;
}

if (document.getElementById('update-venue-form')) {
  document.getElementById('update-venue-form').onsubmit = updateVenue;
}

if (document.getElementById('artist-form')) {
  document.getElementById('artist-form').onsubmit = addNewArtist;
}

if (document.getElementById('update-artist-form')) {
  document.getElementById('update-artist-form').onsubmit = updateArtist;
}


