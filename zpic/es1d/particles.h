/*
 *  particles.h
 *  zpic
 *
 *  Created by Ricardo Fonseca on 11/8/10.
 *  Copyright 2010 Centro de Física dos Plasmas. All rights reserved.
 *
 */

#ifndef __PARTICLES__
#define __PARTICLES__

#include "zpic.h"
#include "field.h"
#include "charge.h"

#include <stdint.h>

/**
 * @brief Maximum species name length
 * 
 */
#define MAX_SPNAME_LEN 32

/**
 * @brief Structure holding single particle data
 * 
 */
typedef struct Particle {
	int ix;		///< Particle cell index
	float x;	///< Position inside cell
	float vx;	///< Velocity along x
} t_part;

/**
 * @brief Types of density profile
 * 
 */
enum density_type {
	UNIFORM,	///< Uniform density
	EMPTY,		///< No particles
	STEP,		///< Step-like profile
	SLAB,		///< Slab-like profile
	RAMP,		///< Density ramp
	CUSTOM		///< Defined from an external function
};

/**
 * @brief Density profile parameters
 * 
 */
typedef struct Density {

	float n;						///< reference density (defaults to 1.0, multiplies density profile)

	enum density_type type;			///< Density profile type
	float start;					///< Start position for step, slab and ramp profiles, in simulation units
	float end;						///< End position for slab and ramp profiles, in simulation units

	float ramp[2]; 					///< Initial and final density of the ramp

	float (*custom)(float, void*); 	///< Custom density function
	void *custom_data; 				///< Additional data to be passed to the custom function

	unsigned long total_np_inj;		///< Total number of particles already injected
	double custom_q_inj;			///< Total charge injected (density integral) in custom profile

} t_density;

/**
 * @brief Set of particles
 * 
 */
typedef struct {
	
	/// Species name
	char name[MAX_SPNAME_LEN+1];
	
	// Particle data
	t_part *part;	///< Particle buffer
	int np;			///< Number of particles in buffer
	int np_max;		///< Maximum number of particles in buffer

	/// mass over charge ratio
	float m_q;
	
	/// charge of individual particle
	float q;

	/// total kinetic energy
	double energy;
	
	/// Number of particles per cell
	int ppc;

	/// Density profile to inject
	t_density density;

	// Initial velocity of particles
	float vfl;	///< Initial fluid velocity of particles
	float vth;	///< Initial thermal velocity of particles

	// Simulation box info
	int nx;		///< Number of grid points
	float dx;	///< Cell size in simulation units
	float box;	///< Simulation box size in simulation units

	/// Time step
	float dt;

	/// Iteration number
	int iter;

	/// Sorting frequency
	int n_sort;

} t_species;

/**
 * @brief Initialize particle Species object
 * 
 * This routine will also inject the initial particle distribution,
 * setting thermal/fluid velocities.
 * 
 * @param spec 		Particle species
 * @param name 		Name for the species (used for diagnostic output)
 * @param m_q 		Mass over charge ratio for species, in simulation units
 * @param ppc 		Reference number of particles per cell
 * @param vfl 		Initial fluid velocity of particles, may be set to NULL 
 * @param vth 		Initial thermal velocity of particles, may be set to NULL
 * @param nx 		Number of grid points
 * @param box 		Simulation box size in simulation units
 * @param dt 		Simulation time step, in simulation units
 * @param density 	Density profile for particle injection, may be set to NULL
 */
void spec_new( t_species* spec, char name[], const float m_q, const int ppc, 
			  const float * vfl, const float * vth,
			  const int nx, float box, const float dt, t_density* density );

/**
 * @brief Frees dynamic memory from particle species
 * 
 * @param spec Particle species
 */
void spec_delete( t_species* spec );

/**
 * @brief Grows particle buffer to specified size.
 * 
 * If the new size is smaller than the previous size the buffer size is not changed
 * and the function returns silently.
 * 
 * @param spec  Particle species
 * @param size  New buffer size (will be rounded up to next multiple of 1024)
 **/
void spec_grow_buffer( t_species* spec, const int size );

/**
 * @brief Advance particle species 1 timestep
 * 
 * Particles are advanced in time using a leap-frog method. Charge
 * deposition is done at the end point of the trajectory.
 * 
 * The routine will also:
 * 1. Calculate total time-centered kinetic energy for the Species
 * 2. Apply boundary conditions
 * 3. Sort particle buffer
 * 
 * 
 * @param spec 		Particle species
 * @param field 	Electric field
 * @param charge 	Charge density
 */
void spec_advance( t_species* spec, t_field* emf, t_charge* charge );

/**
 * @brief Returns the total number of particle pushes
 * 
 * @return  Number of particle pushes
 */
uint64_t spec_npush( void );

/**
 * @brief Returns the total time spent pushing particles
 * 
 * @return  Total time in seconds
 */
double spec_time( void );

/**
 * @brief Returns the performance achieved by the code (push time)
 * 
 * @return  Performance in seconds per particle, -1.0 if no particles were
 *          pushed
 */
double spec_perf( void );

/*********************************************************************************************
 
 Diagnostics
 
 *********************************************************************************************/

#define CHARGE 		0x1000
#define PHA    		0x2000
#define PARTICLES   0x3000
#define X1     		0x0001
#define V1     		0x0004

/**
 * @brief Defines a phasespace density report with the specified quantities
 * 
 * @param a		Phasespace x axis
 * @param b		Phasespace y axis
 * @return int value describing phasespace report
 */
#define PHASESPACE(a,b) ((a) + (b)*16 + PHA)

/**
 * @brief Deposit 2D phasespace density.
 * 
 * @param spec      Particle species
 * @param rep_type  Type of phasespace, use the PHASESPACE macro to define
 * @param pha_nx    Number of grid points in the phasespace density grid
 * @param pha_range Physical range of each of the phasespace axis
 * @param buf       Phasespace density grid
 */
void spec_deposit_pha( const t_species *spec, const int rep_type,
			  const int pha_nx[], const float pha_range[][2], float* buf );

/**
 * @brief Deposits particle species charge density
 * 
 * Deposition is done using linear interpolation. Used for diagnostics
 * purpose only.
 * 
 * @param spec      Particle species
 * @param charge    Electric charge density
 */
void spec_deposit_charge( const t_species* spec, float* charge );

/**
 * @brief Saves particle species diagnostic information to disk
 * 
 * @param spec      Particle species
 * @param rep_type  Type of diagnostic information {CHARGE, PHASESPACE(a,b), PARTICLES}
 * @param pha_nx    Number of grid points in the phasespace density grid, set to NULL for
 *                  diagnostics other then phasespace density
 * @param pha_range Physical range of each of the phasespace axis, set to NULL for
 *                  diagnostics other then phasespace density
 */
void spec_report( const t_species *spec, const int rep_type, 
				  const int pha_nx[], const float pha_range[][2] );


#endif
