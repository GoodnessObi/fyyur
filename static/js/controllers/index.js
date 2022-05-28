
import { addNewVenue } from './new_venue.js';
import { addNewArtist } from './new_artist.js';

if (document.getElementById('venue-form')) {
  document.getElementById('venue-form').onsubmit = addNewVenue;
}

if (document.getElementById('artist-form')) {
  document.getElementById('artist-form').onsubmit = addNewArtist;
}

