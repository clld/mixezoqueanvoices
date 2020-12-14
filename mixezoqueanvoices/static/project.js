// Play sounds from west to east:
CLLD.AudioPlayerOptions.marker_order = function (m1, m2) {
    return m1.getLatLng().lng - m2.getLatLng().lng
}
