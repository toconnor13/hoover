import rpy2.robjects as robjects

robjects.r('''
	get_duration <- function(customer_probereq_file){
		data = read.csv(customer_probereq_file)
		data[4] <- NULL
		colnames(data) <- c('id', 'timestamp', 'rssi')

		# **** IN_OUT CALCULATION ****
			data$in_out <- 0
			data$in_out[data$rssi > -70] <- 1
			N <- length(data$in_out)

			# This code is designed to let the strongest signal dominate in the calculations.
			for(i in 2:N){
				data$in_out[i][data$timestamp[i]-data$timestamp[i-1]<2 && data$in_out[i-1]==1] <- 1 
			}

		#  TIME SINCE LAST PROBE REQUEST -  if 1st PR, default val=72000

			data$since_last_pr <- 0
			data$since_last_pr[1] <- 76000

			for(i in 2:N){
				data$since_last_pr[i] <- data$timestamp[i]-data$timestamp[i-1]
			}

		# CALCULATING IF A NEW VISIT HAS OCCURRED
			data$visit_no <- 1
			for(i in 2:N){
				if(data$since_last_pr[i]>3600){
					data$visit_no[i] <-data$visit_no[i-1] + 1
				}
				else{
					data$visit_no[i] <- data$visit_no[i-1]
				}
			}

		# The following code calculates the duration of the visit.
		data$duration <- 0
		for(i in 2:N){
			if(data$since_last_pr[i]>3600){
				data$duration[i] <- 7
			}
			else{
				data$duration[i] <- data$duration[i-1] + data$timestamp[i] - data$timestamp[i-1]		
			}
		}


		# The following code establishes the time of arrival.

			leave_time <- 0
			for(i in 2:N){
				leave_time[data$in_out[i]==1 && data$in_out[i+1]==0] <- data$timestamp[i]		
			}

		# RESULTS TO SUBMIT
			no_of_visits <- max(data$visit_no)
			uid <- as.character(data$id[1])

			result_matrix <- matrix(0, no_of_visits, 4) 
			result <- NULL
			for(i in 1:no_of_visits){
				duration1 <- max(data$duration[data$visit_no==i])
				arrival_time <- data$timestamp[data$visit_no==i][1]
				leave_time1 <- arrival_time + duration1
				result <- c(result, uid, arrival_time, duration1, leave_time1)
			}

		return(result)
	}
	''')
