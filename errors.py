import numpy as np

from matplotlib import pyplot as plt

from constants import telescope, earth

# https://www.spaceacademy.net.au/watch/track/locgsat.htm

c = 2.997925e5  # km/s

r_geo = (earth.mu*earth.p_sidereal**2 / (4 * np.pi**2))**(1/3)
d_theta = telescope.shutter_t / earth.p_sidereal * 2*np.pi
print(d_theta)

x = r_geo * d_theta

r_t = earth.vec_from_coors(telescope.coors)

sat_range = []
elevation = []
timing_error_px = []
timing_error_km = []
pixel_res = []
test = []

for lon in np.arange(0, 2*np.pi, np.pi/360):
# for lon in [telescope.coors_rad[1]]:
    lons = np.array([lon, lon + d_theta])

    cos_g = np.cos(telescope.coors_rad[0]) * np.cos(lons - telescope.coors_rad[1])
    g = np.arccos(cos_g)

    elev = np.arctan((r_geo * cos_g - earth.r) / (r_geo * np.sin(g)))

    if np.all(elev >= 0):
        r_s = r_geo * np.array([[np.cos(lon), np.sin(lon), 0],
                                [np.cos(lon + d_theta), np.sin(lon + d_theta), 0]])

        r_ts = r_s - r_t

        n_rts = np.linalg.norm(r_ts, axis=1)
        mean_rts = np.mean(n_rts)

        sat_range.append(mean_rts)
        elevation.append(np.degrees(np.mean(elev)))

        cos_nadir = - (earth.r**2 - mean_rts**2 - r_geo**2)/(2 * mean_rts * r_geo)        

        rpx = telescope.fov_pp * mean_rts / cos_nadir
        pixel_res.append(telescope.fov_pp * mean_rts / cos_nadir)

        obs_theta = np.arccos( np.dot(r_ts[0], r_ts[1]) / np.prod(n_rts))
        px_s = obs_theta / telescope.fov_pp / telescope.shutter_t
        
        n_px = px_s * np.arange(-1, 1, 0.2) * telescope.shutter_dt
        timing_error_px.append(n_px)
        timing_error_km.append(n_px*rpx)

        # print(np.degrees(lon))

pixel_res = 1000*np.array(pixel_res)
timing_error_px = np.array(timing_error_px)
timing_error_km = np.array(timing_error_km)

plt.figure(1)
plt.plot(elevation, pixel_res)
plt.title("End point detection pixel error")
plt.xlabel("Elevation [deg]")
plt.ylabel("Error [m]")
plt.savefig("figures/endpoint")

plt.figure(2)
plt.plot(elevation, timing_error_px)
plt.title("Error due to shutter offset")
plt.xlabel("Elevation [deg]")
plt.ylabel("Error [px]")
plt.legend(np.round(np.arange(-1, 1, 0.2) * telescope.shutter_dt, 3))
plt.savefig("figures/timingpx")

plt.figure(3)
plt.plot(elevation, 1000*timing_error_km)
plt.title("Error due to shutter offset")
plt.xlabel("Elevation [deg]")
plt.ylabel("Error [m]")
plt.legend(np.round(np.arange(-1, 1, 0.2) * telescope.shutter_dt, 3))
plt.savefig("figures/timingm")

plt.figure(4)
plt.plot(elevation, np.array(sat_range)/c)
plt.title("Light-time effect")
plt.xlabel("Elevation [deg]")
plt.ylabel("Light travel time [s]")
plt.savefig("figures/lighttime")

plt.show()
