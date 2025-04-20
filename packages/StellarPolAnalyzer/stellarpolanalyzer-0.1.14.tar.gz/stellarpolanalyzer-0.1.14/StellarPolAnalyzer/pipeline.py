# File: pipeline.py
"""
Pipeline orchestration for StellarPolAnalyzer:
- compute_full_polarimetry: polarimetric processing of 4 FITS
- run_complete_polarimetric_pipeline: full pipeline including astrometry and reporting
"""
import os
import astropy.units as u
import matplotlib.pyplot as plt
from .detection import process_image
from .alignment import align_images, save_fits_with_same_headers
from .photometry import compute_polarimetry_for_pairs
from .astrometry import annotate_with_astrometry_net
from .visualization import draw_pairs


def compute_full_polarimetry(ref_path, other_paths,
                             fwhm=3.0, threshold_multiplier=5.0,
                             tol_distance=0.52, tol_angle=0.30,
                             max_distance=75,
                             phot_aperture_radius=5, r_in=7, r_out=10, SNR_threshold=5,
                             save_plots=False, report_dir=None):
    """
    Process 4 polarimetric images: alignment, pairing, and photometry.

    Optional reporting: if save_plots=True and report_dir provided,
    saves intermediate plots in report_dir.
    """
    # prepare report directory
    if save_plots and report_dir:
        os.makedirs(report_dir, exist_ok=True)

    # 1) Align images
    ref_data = __import__('astropy.io.fits').io.fits.getdata(ref_path)
    final_paths = [ref_path]
    for path in other_paths:
        img_data = __import__('astropy.io.fits').io.fits.getdata(path)
        aligned, shift_vec = align_images(ref_data, img_data)
        out_fits = path.replace('.fits', '-aligned.fits')
        save_fits_with_same_headers(path, aligned, out_fits)
        final_paths.append(out_fits)
        if save_plots and report_dir:
            # plot alignment result
            fig, ax = plt.subplots(figsize=(6,6))
            ax.imshow(aligned, cmap='gray', origin='lower')
            ax.set_title(f"Aligned: {os.path.basename(path)}\nShift: {shift_vec}")
            fig.savefig(os.path.join(report_dir, f"align_{os.path.basename(path)}.png"), bbox_inches='tight')
            plt.close(fig)

    # 2) Detect & pair
    process_results = []
    for path in final_paths:
        res = process_image(path,
                            fwhm=fwhm,
                            threshold_multiplier=threshold_multiplier,
                            tol_distance=tol_distance,
                            tol_angle=tol_angle,
                            max_distance=max_distance)
        process_results.append(res)
        if save_plots and report_dir:
            # save pair plot for each image
            img_data, sources, _, pairs, d_mode, a_mode = res
            plot_name = os.path.join(report_dir, f"pairs_{os.path.basename(path).replace('.fits','.png')}")
            draw_pairs(img_data, sources, pairs,
                       num_stars=len(sources),
                       mode_distance=d_mode, mode_angle=a_mode,
                       tol_distance=tol_distance, tol_angle=tol_angle,
                       save_path=plot_name)

    # 3) Photometry & polarimetry on reference
    _, sources, _, final_pairs, _, _ = process_results[0]
    polar_results = compute_polarimetry_for_pairs(
        final_paths, sources, final_pairs,
        aperture_radius=phot_aperture_radius,
        r_in=r_in, r_out=r_out,
        SNR_threshold=SNR_threshold
    )

    return process_results, polar_results, final_paths


def run_complete_polarimetric_pipeline(ref_path, other_paths, pol_angles,
                                        fwhm=3.0,
                                        threshold_multiplier=5.0,
                                        tol_distance=0.52,
                                        tol_angle=0.30,
                                        max_distance=75,
                                        phot_aperture_radius=5,
                                        r_in=7,
                                        r_out=10,
                                        SNR_threshold=5,
                                        astrometry_api_key=None,
                                        simbad_radius=0.01*u.deg,
                                        synthetic_name="synthetic.fits",
                                        save_plots=False,
                                        report_dir=None):
    """
    Full polarimetric + astrometric pipeline, with optional report generation.

    Parameters save_plots/report_dir cascade to compute_full_polarimetry and annotate.
    """
    # Polarimetry steps + reporting
    process_results, polar_results, final_paths = compute_full_polarimetry(
        ref_path, other_paths,
        fwhm=fwhm,
        threshold_multiplier=threshold_multiplier,
        tol_distance=tol_distance,
        tol_angle=tol_angle,
        max_distance=max_distance,
        phot_aperture_radius=phot_aperture_radius,
        r_in=r_in, r_out=r_out,
        SNR_threshold=SNR_threshold,
        save_plots=save_plots,
        report_dir=report_dir
    )

    # Extract reference sources & pairs
    _, sources, _, final_pairs, _, _ = process_results[0]

    # Astrometry & SIMBAD
    wcs, enriched = annotate_with_astrometry_net(
        ref_path,
        sources,
        final_pairs,
        polar_results,
        fwhm=fwhm,
        api_key=astrometry_api_key,
        simbad_radius=simbad_radius,
        synthetic_name=synthetic_name
    )

    return final_paths, polar_results, wcs, enriched
