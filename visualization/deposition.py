import numpy as np

def accumulate_deposition(field, sample_times, current_time, dispensing, sample_x, sample_y, drift_x, drift_y, X, Y, amplitude, sigma, dt):
    for i in range(len(sample_times)):

        if sample_times[i] > current_time:
            break

        if not dispensing[i]:
            continue

        # Wind shifts the center of each deposition footprint
        center_x = sample_x[i] + drift_x
        center_y = sample_y[i] + drift_y

        gaussian = amplitude * np.exp(
            -(
                (X - center_x)**2 +
                (Y - center_y)**2
            ) / (2 * sigma**2)
        )

        field += gaussian * dt
    return field
